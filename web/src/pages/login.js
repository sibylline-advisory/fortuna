import {DynamicWidget} from "@dynamic-labs/sdk-react-core";
import {createSmartAccountClient, ENTRYPOINT_ADDRESS_V06, walletClientToSmartAccountSigner,} from "permissionless";
import {signerToSimpleSmartAccount} from "permissionless/accounts";
import {sponsorUserOperation} from "permissionless/actions/pimlico";
import {useWalletClient} from "wagmi";
import {baseSepolia} from "viem/chains";
import {zeroAddress, http, createPublicClient} from "viem";

export default function Login() {

	const {data} = useWalletClient();
	console.log(data)

	const createSmartAccount = async () => {
		const signer = walletClientToSmartAccountSigner(data)
		console.log("Signer", signer)
		const publicClient = createPublicClient({
			chain: baseSepolia, // or whatever chain you are using
			transport: http("https://sepolia.base.org/"),
		})
		console.log("Public client", publicClient)
		const simpleSmartAccountClient = await signerToSimpleSmartAccount(
			publicClient,
			{
				entryPoint: "0x5FF137D4b0FDCD49DcA30c7CF57E578a026d2789",
				signer: signer,
				factoryAddress: "0x9406Cc6185a346906296840746125a0E44976454",
			}
		);
		console.log("Simple smart account client", simpleSmartAccountClient)
		const smartAccountClient = createSmartAccountClient({
			account: simpleSmartAccountClient,
			chain: baseSepolia, // or whatever chain you are using
			bundlerTransport: http("https://api.pimlico.io/v2/base-sepolia/rpc?apikey=cb041e12-7980-4c33-9d3f-f8e0fd3172b7"),
			entryPoint: ENTRYPOINT_ADDRESS_V06,
			middleware: {
				sponsorUserOperation: sponsorUserOperation, // optional, if using a paymaster
			},
		})
		console.log("Smart account client", smartAccountClient)
		// down from here borked.
		const txHash = await smartAccountClient.sendTransaction({
			to: zeroAddress,
			data: "0x",
			value: BigInt(0)
		})

		console.log(txHash)
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