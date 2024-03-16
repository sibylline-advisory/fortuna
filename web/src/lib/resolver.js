import {encodeFunctionData, getContract} from 'viem'
import {pimlicoBundlerClient, publicClient} from "@/lib/pimlico";
import {ENTRYPOINT_ADDRESS_V06} from "permissionless";
import {getTask, patchTask} from "@/lib/task";

export const getResolution = async (tid) => {
	const response = await getTask(tid)
	console.log("response", response)
	// TODO finish impl.
	// USDC resolution response.
	return {
		abi: [{
			"inputs": [{"internalType": "address", "name": "to", "type": "address"}, {
				"internalType": "uint256",
				"name": "value",
				"type": "uint256"
			}],
			"name": "transfer",
			"outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
			"stateMutability": "nonpayable",
			"type": "function"
		}, {
			"inputs": [{"internalType": "address", "name": "account", "type": "address"}],
			"name": "balanceOf",
			"outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
			"stateMutability": "view",
			"type": "function"
		}, {
			"inputs": [],
			"name": "decimals",
			"outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
			"stateMutability": "view",
			"type": "function"
		}],
		args: [
			"0x8f56A5cF7c56a01118d2C5992146473D32b5f612", // harper safe account
			1000000
		],
		address: "0x036CbD53842c5426634e7929541eC2318f3dCF7e",
	}
}

export const handleAgentResolution = async (data, signer, safeAccount, smartAccountClient) => {
	console.log("data", data)
	console.log("signer", signer)
	console.log("safeAccount", safeAccount)
	console.log("smartAccountClient", smartAccountClient)
	const callData = await safeAccount.current.encodeCallData({
		to: data.address,
		data: encodeFunctionData({
				abi: data.abi,
				args: data.args,
			},
		),
		value: 0n
	})
	console.log('callData', callData)
	const userOperation = await smartAccountClient.current.prepareUserOperationRequest({
		userOperation: {
			callData
		}
	})
	console.log('userOperation', userOperation)
	const userOpHash = await smartAccountClient.current.sendUserOperation({
		userOperation,
		entryPoint: ENTRYPOINT_ADDRESS_V06
	})
	console.log('userOpHash', userOpHash)
	return {hash: userOpHash} // the hash?
}


export const ackAgentResolution = async (tid, data, jwt) => {
	const apiResponse = await patchTask(tid, {op_hash: data}, jwt)
	console.log("apiResponse", apiResponse)
	return {}
}