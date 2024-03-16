/**
 * This code was generated by v0 by Vercel.
 * @see https://v0.dev/t/8XCAUq2ZoxN
 */
import Image from "next/image";
import {useEffect, useRef, useState} from "react";
import {Input} from "@/components/ui/input";
import {sendTask} from "@/lib/task";
import {useWalletClient} from "wagmi";
import TestButtons from "@/components/TestButtons";
import WalletModalWrapper from "@/components/WalletModalWrapper";
import {getAuthToken} from "@dynamic-labs/sdk-react-core";
import {ackAgentResolution, getResolution, handleAgentResolution} from "@/lib/resolver";
import {doClientSetup} from "@/lib/pimlico";

export function Index() {
	const [message, setMessage] = useState("");
	const {data} = useWalletClient();
	const signer = useRef({})
	const safeAccount = useRef({})
	const smartAccountClient = useRef({})

	const [loading, setLoading] = useState(false);

	const [resolutionDetails, setResolutionDetails] = useState(null);
	const [hasResolution, setHasResolution] = useState(false);

	useEffect(() => {
		const pollApi = async () => {
			const response = await getResolution(hasResolution.tid);
			if (response) {
				console.log("Got resolution response", response)
				setResolutionDetails(response);
			}
		};
		let intervalId;
		if (hasResolution && !resolutionDetails) {
			console.log(`Resolution: ${JSON.stringify(hasResolution)} - polling`);
			intervalId = setInterval(pollApi, 1000);
		}

		return () => {
			clearInterval(intervalId); // Clean up the interval on component unmount
		};
	}, [hasResolution, resolutionDetails]);

	useEffect(() => {
		if (resolutionDetails) {
			console.log("useEffect -> pollData", resolutionDetails)
			doClientSetup(data, signer, safeAccount, smartAccountClient).then(() => {
				console.log("client setup done");
				handleAgentResolution(resolutionDetails, signer, safeAccount, smartAccountClient).then((r) => {
					console.log("Handled resolution")
					ackAgentResolution(hasResolution.tid, r.hash, getAuthToken()).then(() => {
						console.log("acknowledged")
						setResolutionDetails(null);
						setHasResolution(false);
					});
				});
			});
		}
	}, [data, resolutionDetails])

	// console.log("Index -> data", data)

	const submit = async () => {
		console.log(message);
		const response = await sendTask(message, getAuthToken());
		console.log(response);
		if (response) {
			console.log("has resolution")
			setHasResolution(response);
		}
	}

	const formHandler = (e) => {
		e.preventDefault();
		if (message.trim() === "") return;
		setLoading(true);
		submit().then(() => {
			console.log("handled")
		});
		setMessage("");
		setLoading(false);
	}

	return (
		<div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 dark:bg-gray-900">
			<div className="absolute top-0 left-0 right-0 flex items-center justify-between p-4">
				<div className="flex items-center">
					<Image
						width={10}
						height={10}
						alt="Logo"
						className="w-10 h-10"
						src="/placeholder.svg"
					/>
					<div className="ml-2 text-2xl font-semibold text-gray-800 dark:text-gray-200">
						Fortuna
					</div>
				</div>
				<div className="flex items-center">
					<WalletModalWrapper/>
				</div>
			</div>
			<div className="flex flex-col items-center justify-center gap-4">
				<div className="text-4xl font-bold text-gray-700 dark:text-gray-300">
					Welcome to Fortuna
				</div>
				<div className="text-lg text-gray-600 dark:text-gray-400">
					Your on-chain money manager
				</div>
				<div className="flex items-center w-full max-w-md p-2 bg-white dark:bg-gray-800 rounded-full shadow-md">
					<Image
						width={32}
						height={32}
						alt="Search Icon"
						className="w-6 h-6 ml-2 text-gray-500"
						src="/placeholder.svg"
					/>
					<form onSubmit={formHandler}>
						{!loading ? <Input
								className="w-full p-2 ml-4 text-lg text-gray-700 dark:text-gray-300 bg-transparent outline-none"
								placeholder="Lets get started"
								type="text"
								value={message}
								onChange={(e) => setMessage(e.target.value)}
							/> :
							<Input
								disbled
								className="w-full p-2 ml-4 text-lg text-gray-700 dark:text-gray-300 bg-transparent outline-none"
								type="text"
								value={message}
							/>
						}
					</form>
				</div>
				<TestButtons data={data} signer={signer} safeAccount={safeAccount}
				             smartAccountClient={smartAccountClient}/>
			</div>
		</div>
	);
}
