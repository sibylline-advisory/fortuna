import "@/styles/globals.css";
import {DynamicContextProvider} from '@dynamic-labs/sdk-react-core';
import {EthereumWalletConnectors} from "@dynamic-labs/ethereum";
import {DynamicWagmiConnector} from "@dynamic-labs/wagmi-connector";

export default function App({Component, pageProps}) {
	return (

		<DynamicContextProvider
			settings={{
				environmentId: 'b1c47bc4-7e96-451e-a937-f85fa7226bfb',
				walletConnectors: [EthereumWalletConnectors],
			}}>
	      <DynamicWagmiConnector>
				<Component {...pageProps} />
			</DynamicWagmiConnector>
		</DynamicContextProvider>
	)
}
