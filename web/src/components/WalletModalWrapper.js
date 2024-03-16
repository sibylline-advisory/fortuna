import {DynamicWidget} from "@dynamic-labs/sdk-react-core";
import {doClientSetup, safeSendTxn} from "@/lib/pimlico";
import {parseEther, zeroAddress} from "viem";

export default function WalletModalWrapper() {
	return (
		<>
			<DynamicWidget/>
		</>
	)
}