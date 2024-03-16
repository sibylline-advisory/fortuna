import {doClientSetup, safeSendTxn} from "@/lib/pimlico";
import {parseEther, zeroAddress} from "viem";

export default function TestButtons(data, signer, safeAccount, smartAccountClient) {

	const demoSendEth = {
		to: "0xaf785f9296741a3BAF34eA2A6b576ACAFA30B6Ec", // 3266miles.eth
		value: parseEther("0.001")
	}

	const createSmartAccount = async () => {
		console.log("data", data)
		try {
			await doClientSetup(data, signer, safeAccount, smartAccountClient)
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

	const sendSafeEthHandler = (e) => {
		e.preventDefault()
		safeSendTxn(demoSendEth, data, signer, safeAccount, smartAccountClient).then(() => {
			console.log("SAFE ETH sent")
		}).catch((e) => {
			console.error(e)
		})
	}

	return (
		<>
			<button onClick={createWalletHandler}>Create Wallet</button>
			<div className={"flex-1"}>
				<button onClick={sendSafeEthHandler}>Send SAFE ETH</button>
			</div>
		</>
	)
}