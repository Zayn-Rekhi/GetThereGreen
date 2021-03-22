import { Typography, Container, Snackbar } from '@material-ui/core';
import React from 'react';
import Alert from './Alert';
import { useState } from 'react';
import Loading from './Loading';
import Fields from './Fields';
import Chart from './Chart';
import fetchWithTimeout from './BetterFetch';

interface ApiData {
	summary: string;
	max: number;
	predictions: {
		CarbonMonoxide: number[];
		NitrogenDioxide: number[];
		Ozone: number[];
		SulfurDioxide: number[];
	};
}

export default function Graph() {
	const [max, changeMax] = useState(400);
	const [loadingFlag, updateLoadingFlag] = useState(false);
	const [summary, ChangeSummary] = useState('');
	const [data, updateData] = useState({
		NitrogenDioxide: [
			{ x: 1, y: 2 },
			{ x: 2, y: 3 },
			{ x: 3, y: 3 },
			{ x: 4, y: 3 },
			{ x: 6, y: 3 },
			{ x: 7, y: 3 },
			{ x: 8, y: 3 },
			{ x: 9, y: 3 },
			{ x: 10, y: 3 },
		],
		SulfurDioxide: [
			{ x: 1, y: 2 },
			{ x: 2, y: 3 },
			{ x: 3, y: 3 },
			{ x: 4, y: 3 },
			{ x: 6, y: 3 },
			{ x: 7, y: 3 },
			{ x: 8, y: 3 },
			{ x: 9, y: 3 },
			{ x: 10, y: 3 },
		],
		Ozone: [
			{ x: 1, y: 2 },
			{ x: 2, y: 3 },
			{ x: 3, y: 3 },
			{ x: 4, y: 3 },
			{ x: 6, y: 3 },
			{ x: 7, y: 3 },
			{ x: 8, y: 3 },
			{ x: 9, y: 3 },
			{ x: 10, y: 3 },
		],
		CarbonMonoxide: [
			{ x: 1, y: 2 },
			{ x: 2, y: 3 },
			{ x: 3, y: 3 },
			{ x: 4, y: 3 },
			{ x: 6, y: 3 },
			{ x: 7, y: 3 },
			{ x: 8, y: 3 },
			{ x: 9, y: 3 },
			{ x: 10, y: 3 },
		],
	});

	const fetchData = async (nofuel: number, publict: number, solo: number) => {
		updateLoadingFlag(true);
		const requestOptions = {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				'no-fuel': nofuel, //add the current values from the input fields to the request's body
				public: publict,
				cars: solo,
				years: 'default',
			}),
		};
		try {
			const response = await fetchWithTimeout(
				'https://api.gettheregreen.ml',
				requestOptions
			);
			console.log(response);
			if (response.status !== 200) {
				handleClick();
				return;
			}
			response.json().then((apidata: ApiData) => {
				interface ValPair {
					x: number;
					y: number;
				}
				interface DataIN {
					CarbonMonoxide: ValPair[];
					NitrogenDioxide: ValPair[];
					SulfurDioxide: ValPair[];
					Ozone: ValPair[];
				}
				let datin: DataIN = {
					CarbonMonoxide: [],
					NitrogenDioxide: [],
					SulfurDioxide: [],
					Ozone: [],
				};
				changeMax(Math.ceil(apidata.max / 10) * 10);
				// eslint-disable-next-line
				apidata.predictions.CarbonMonoxide.map((e: number, i: number) => {
					if (i < 10) {
						datin.CarbonMonoxide.push({ x: i + 1, y: e });
					}
				});
				// eslint-disable-next-line
				apidata.predictions.SulfurDioxide.map((e: number, i: number) => {
					if (i < 10) {
						datin.SulfurDioxide.push({ x: i + 1, y: e });
					}
				});
				// eslint-disable-next-line
				apidata.predictions.Ozone.map((e: number, i: number) => {
					if (i < 10) {
						datin.Ozone.push({ x: i + 1, y: e });
					}
				});
				// eslint-disable-next-line
				apidata.predictions.NitrogenDioxide.map((e: number, i: number) => {
					if (i < 10) {
						datin.NitrogenDioxide.push({ x: i + 1, y: e });
					}
				});
				updateData(datin);
				ChangeSummary(apidata.summary);
				updateLoadingFlag(false);
			});
		} catch {
			handleClick();
			updateLoadingFlag(false);
		}
	};

	const [open, setOpen] = useState(false);
	const handleClick = () => {
		setOpen(true);
	};
	const handleClose = (event?: React.SyntheticEvent, reason?: string) => {
		if (reason === 'clickaway') {
			return;
		}

		setOpen(false);
	};

	return (
		<div>
			<Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
				<Alert onClose={handleClose} severity='error'>
					Uh oh! Something is wrong with our servers. Please check back later.
				</Alert>
			</Snackbar>
			<Container style={{ textAlign: 'center', width: '100%' }}>
				<Typography variant='h2'>Predicted Air Quality</Typography>
			</Container>
			<Chart max={max} data={data} />
			<br />
			<Loading visibility={loadingFlag} />
			<Fields loadingFlag={loadingFlag} fetchData={fetchData} />
			<br />
			<Typography variant='h3'>{summary !== '' ? 'Summary: ' : ''}</Typography>
			<Typography variant='body1'>{summary}</Typography>
		</div>
	);
}
