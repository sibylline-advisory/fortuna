import {DynamicWidget} from "@dynamic-labs/sdk-react-core";
import {createSmartAccountClient, ENTRYPOINT_ADDRESS_V06, walletClientToSmartAccountSigner,} from "permissionless";
import {signerToSafeSmartAccount} from "permissionless/accounts";
import {useWalletClient} from "wagmi";
import {baseSepolia} from "viem/chains";
import {http, parseEther, zeroAddress} from "viem";
import {paymasterClient, pimlicoBundlerClient, pimlicoRPC, publicClient} from "@/lib/pimlico";
import {useEffect, useRef} from "react";

export default function Login() {

	const {data} = useWalletClient();
	const signer = useRef({})
	const safeAccount = useRef({})
	const smartAccountClient = useRef({})


	const doClientSetup = async () => {
		if (!data) {
			throw new Error("No wallet data")
		}
		signer.current = walletClientToSmartAccountSigner(data)
		safeAccount.current = await signerToSafeSmartAccount(publicClient, {
			entryPoint: ENTRYPOINT_ADDRESS_V06,
			signer: signer.current,
			safeVersion: "1.4.1",
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

	const createSmartAccount = async () => {
		console.log("data", data)
		try {
			await doClientSetup()
			// unsure if this does what we want it to.
			const txHash = await smartAccountClient.current.sendTransaction({
				to: zeroAddress,
				data: "0x",
				value: parseEther("0")
			})
			console.log(txHash)
		} catch (e) {
			console.error(e)
		}
	}

	const createWalletHandler = (e) => {
		e.preventDefault()
		createSmartAccount().then(() => {
			console.log("Smart account created")
		}).catch((e) => {
			console.error(e)
		})
	}

	const safeSendTxn = async (txn) => {
		const gasPrices = await pimlicoBundlerClient.getUserOperationGasPrice()
		console.log("Gas prices", gasPrices)
		txn.maxFeePerGas = gasPrices.fast.maxFeePerGas
		txn.maxPriorityFeePerGas = gasPrices.fast.maxPriorityFeePerGas
		try {
			await doClientSetup()
			console.log(smartAccountClient)
			const txHash = await smartAccountClient.current.sendTransaction(txn)
			console.log(txHash)
		} catch (e) {
			console.error(e)
		}
	}

	const sendSafeEthHandler = (e) => {
		e.preventDefault()
		const demoSendEth = {
			to: "0xaf785f9296741a3BAF34eA2A6b576ACAFA30B6Ec", // 3266miles.eth
			value: parseEther("0.001")
		}
		safeSendTxn(demoSendEth).then(() => {
			console.log("SAFE ETH sent")
		}).catch((e) => {
			console.error(e)
		})
	}


	return (
		<div className={"p-4 flex"}>
			<DynamicWidget/>
			<button onClick={createWalletHandler}>Create Wallet</button>
			<div className={"flex-1"}>
				<button onClick={sendSafeEthHandler}>Send SAFE ETH</button>
			</div>
		</div>
	)
}