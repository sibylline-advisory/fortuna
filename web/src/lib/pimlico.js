import {createPublicClient, http} from "viem";
import {baseSepolia} from "viem/chains";
import {createPimlicoBundlerClient, createPimlicoPaymasterClient} from "permissionless/clients/pimlico";
import {createSmartAccountClient, ENTRYPOINT_ADDRESS_V06, walletClientToSmartAccountSigner} from "permissionless";
import {signerToSafeSmartAccount} from "permissionless/accounts";
import {getCookie, setCookie} from "cookies-next";

export const pimlicoRPC = "https://api.pimlico.io/v2/base-sepolia/rpc?apikey=cb041e12-7980-4c33-9d3f-f8e0fd3172b7"

export const publicClient = createPublicClient({
	chain: baseSepolia, // or whatever chain you are using
	transport: http("https://sepolia.base.org/"),
})

export const paymasterClient = createPimlicoPaymasterClient({
	transport: http(pimlicoRPC),
	entryPoint: ENTRYPOINT_ADDRESS_V06,
})

export const pimlicoBundlerClient = createPimlicoBundlerClient({
	transport: http(pimlicoRPC),
	entryPoint: ENTRYPOINT_ADDRESS_V06,
})

export const doClientSetup = async (data, signer, safeAccount, smartAccountClient) => {
	if (!data) {
		throw new Error("No wallet data")
	}
	signer.current = walletClientToSmartAccountSigner(data)
	safeAccount.current = await signerToSafeSmartAccount(publicClient, {
		entryPoint: ENTRYPOINT_ADDRESS_V06,
		signer: signer.current,
		safeVersion: "1.4.1",
	})
	setCookie("safe_addr", safeAccount.current.address, {
		maxAge: 60 * 60 * 24 * 7,
		path: "/",
	})
	smartAccountClient.current = createSmartAccountClient({
		account: safeAccount.current,
		chain: baseSepolia, // or whatever chain you are using
		bundlerTransport: http(pimlicoRPC),
		entryPoint: ENTRYPOINT_ADDRESS_V06,
		middleware: {
			gasPrice: async () => (await pimlicoBundlerClient.getUserOperationGasPrice()).fast, // use pimlico bundler to get gas prices
			sponsorUserOperation: paymasterClient.sponsorUserOperation, // optional
		},
	})

}


export const safeSendTxn = async (txn, data, signer, safeAccount, smartAccountClient) => {
	const gasPrices = await pimlicoBundlerClient.getUserOperationGasPrice()
	console.log("Gas prices", gasPrices)
	txn.maxFeePerGas = gasPrices.fast.maxFeePerGas
	txn.maxPriorityFeePerGas = gasPrices.fast.maxPriorityFeePerGas
	try {
		console.log(data, signer, safeAccount, smartAccountClient)
		await doClientSetup(data, signer, safeAccount, smartAccountClient)
		console.log(smartAccountClient)
		const txHash = await smartAccountClient.current.sendTransaction(txn)
		console.log(txHash)
	} catch (e) {
		console.error(e)
	}
}