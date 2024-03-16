import {encodeFunctionData, getContract} from 'viem'
import {pimlicoBundlerClient, publicClient} from "@/lib/pimlico";
import {ENTRYPOINT_ADDRESS_V06} from "permissionless";
import {getTask, patchTask} from "@/lib/task";

export const getResolution = async (tid) => {
	const response = await getTask(tid)
	console.log("response", response)
	return JSON.parse(response.call_data)
}

export const handleAgentResolution = async (data, signer, safeAccount, smartAccountClient) => {
	console.log("data", data)
	console.log("signer", signer)
	console.log("safeAccount", safeAccount)
	console.log("smartAccountClient", smartAccountClient)
	const parsedData = JSON.parse(data)
	const fd = {
		abi: parsedData.abi,
		args: parsedData.args,
	}
	console.log("fd", fd)
	const callData = await safeAccount.current.encodeCallData({
		to: parsedData.contract,
		data: encodeFunctionData(fd),
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