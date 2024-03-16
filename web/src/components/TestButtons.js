import {doClientSetup, safeSendTxn} from "@/lib/pimlico";
import {parseEther, zeroAddress} from "viem";

export default function TestButtons({data, signer, safeAccount, smartAccountClient}) {

	const demoSendEth = {
		to: "0x8f56A5cF7c56a01118d2C5992146473D32b5f612", // harper safe
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
		console.log("data", data)
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