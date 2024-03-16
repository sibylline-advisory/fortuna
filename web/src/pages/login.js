import {DynamicWidget} from "@dynamic-labs/sdk-react-core";
import {createSmartAccountClient, ENTRYPOINT_ADDRESS_V06, walletClientToSmartAccountSigner,} from "permissionless";
import {signerToSafeSmartAccount} from "permissionless/accounts";
import {createPimlicoPaymasterClient, createPimlicoBundlerClient} from "permissionless/clients/pimlico"
import {useWalletClient} from "wagmi";
import {baseSepolia} from "viem/chains";
import {createPublicClient, http, zeroAddress} from "viem";

export default function Login() {

	const {data} = useWalletClient();
	const pimlicoRPC = "https://api.pimlico.io/v2/base-sepolia/rpc?apikey=cb041e12-7980-4c33-9d3f-f8e0fd3172b7"

	const createSmartAccount = async () => {
		console.log("data", data)
		const signer = walletClientToSmartAccountSigner(data)
		console.log("Signer", signer)


		const publicClient = createPublicClient({
			chain: baseSepolia, // or whatever chain you are using
			transport: http("https://sepolia.base.org/"),
		})
		console.log("Public client", publicClient)

		const paymasterClient = createPimlicoPaymasterClient({
			transport: http(pimlicoRPC),
			entryPoint: ENTRYPOINT_ADDRESS_V06,
		})
		console.log("Paymaster client", paymasterClient)

		const pimlicoBundlerClient = createPimlicoBundlerClient({
			transport: http(pimlicoRPC),
			entryPoint: ENTRYPOINT_ADDRESS_V06,
		})

		const safeAccount = await signerToSafeSmartAccount(publicClient, {
			entryPoint: ENTRYPOINT_ADDRESS_V06,
			signer: signer,
			safeVersion: "1.4.1",
		})
		console.log("Safe account", safeAccount)

		const smartAccountClient = createSmartAccountClient({
			account: safeAccount,
			chain: baseSepolia, // or whatever chain you are using
			bundlerTransport: http(pimlicoRPC),
			entryPoint: ENTRYPOINT_ADDRESS_V06,
			middleware: {
				gasPrice: async () => (await pimlicoBundlerClient.getUserOperationGasPrice()).fast, // use pimlico bundler to get gas prices
				sponsorUserOperation: paymasterClient.sponsorUserOperation, // optional
			},
		})
		console.log("Smart account client", smartAccountClient)

		const gasPrices = await pimlicoBundlerClient.getUserOperationGasPrice()
		console.log("Gas prices", gasPrices)
		try {
			const txHash = await smartAccountClient.sendTransaction({
				to: zeroAddress,
				data: "0x",
				value: BigInt(0),
				maxFeePerGas: gasPrices.fast.maxFeePerGas, // if using Pimlico
				maxPriorityFeePerGas: gasPrices.fast.maxPriorityFeePerGas, // if using Pimlico
			})
			console.log(txHash)
		} catch (e) {
			console.error(e)
		}
	}

	const onClick = (e) => {
		e.preventDefault()
		createSmartAccount().then(() => {
			console.log("Smart account created")
		}).catch((e) => {
			console.error(e)
		})
	}


	return (
		<div>
			<DynamicWidget/>
			<button onClick={onClick}>Create Wallet</button>
		</div>
	)
}