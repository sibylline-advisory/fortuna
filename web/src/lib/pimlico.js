import {createPublicClient, http} from "viem";
import {baseSepolia} from "viem/chains";
import {createPimlicoBundlerClient, createPimlicoPaymasterClient} from "permissionless/clients/pimlico";
import {ENTRYPOINT_ADDRESS_V06} from "permissionless";

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