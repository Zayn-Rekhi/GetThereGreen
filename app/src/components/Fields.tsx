import {
	Typography,
	Button,
	TextField,
	Grid,
	Paper,
	InputAdornment,
	Hidden,
	Snackbar,
} from '@material-ui/core';
import { useState } from 'react';
import Alert from './Alert';
interface FieldsProps {
	fetchData: (nofuel: number, publict: number, solo: number) => {};
	loadingFlag: boolean;
}

export default function Fields(props: FieldsProps) {
	const [nofuel_transport, changeNoFuel] = useState(34);
	const [public_transport, changePublic] = useState(33);
	const [solo_transport, changeSolo] = useState(33);
	const [open, setOpen] = useState(false);
	const handleClick = () => {
		setOpen(true);
	};
	/**
	 * @param A, B, C values that need to add up to 100
	 * @return A, B, C that add up to 100
	 * */
	const cleanup = (A: number, B: number, C: number): number[] => {
		const T = A + B + C;
		const newA = Math.floor((A / T) * 100);
		const newB = Math.floor((B / T) * 100);
		let newC = Math.floor((C / T) * 100);
		newC += 100 - (newA + newB + newC);
		return [newA, newB, newC];
	};
	const handleClose = (event?: React.SyntheticEvent, reason?: string) => {
		if (reason === 'clickaway') {
			return;
		}

		setOpen(false);
	};
	const calculate = (nofuel: number, publict: number, solo: number) => () => {
		if (nofuel + publict + solo !== 100) {
			const [newA, newB, newC] = cleanup(nofuel, publict, solo);
			nofuel = newA;
			publict = newB;
			solo = newC;
			handleClick();
		}
		changeNoFuel(nofuel);
		changePublic(publict);
		changeSolo(solo);
		props.fetchData(nofuel, publict, solo);
	};
	const adjustInputField = (
		value: number,
		dispatch: React.Dispatch<React.SetStateAction<number>>
	) => {
		if (value >= 0 && value < 100) {
			dispatch(value);
		}
	};
	return (
		<div>
			{/* <Snackbar open={open} autoHideDuration={6000} onClose={handleClose}>
				<Alert onClose={handleClose} severity='warning'>
					Your values were rounded so they add up to 100%
				</Alert>
			</Snackbar> */}
			<Grid justify='center' container spacing={1} alignContent='center'>
				{/* <Grid item xs={2}></Grid> */}

				<Grid style={{ textAlign: 'center' }} item lg={3} md={3} xs={10}>
					<Typography gutterBottom>No-Fuel Transportation</Typography>
					<TextField
						value={nofuel_transport}
						onChange={(e) => {
							if (e.target.value == '') {
								changeNoFuel(NaN);
							} else {
							}
							adjustInputField(parseFloat(e.target.value), changeNoFuel);
						}}
						label='% Bike / Walk'
						type='number'
						InputProps={{
							endAdornment: <InputAdornment position='end'>%</InputAdornment>,
						}}
						InputLabelProps={{
							shrink: true,
						}}
					/>
				</Grid>

				<Grid style={{ textAlign: 'center' }} item lg={3} md={3} xs={10}>
					<Typography gutterBottom>Public Transportation</Typography>
					<TextField
						value={public_transport}
						onChange={(e) => {
							if (e.target.value == '') {
								changePublic(NaN);
							} else {
							}
							adjustInputField(parseFloat(e.target.value), changePublic);
						}}
						label='% Bus / Train'
						type='number'
						InputProps={{
							endAdornment: <InputAdornment position='end'>%</InputAdornment>,
						}}
						InputLabelProps={{
							shrink: true,
						}}
					/>
				</Grid>

				<Grid style={{ textAlign: 'center' }} item lg={3} md={3} xs={10}>
					<Typography gutterBottom>Solo Transportation</Typography>
					<TextField
						value={solo_transport}
						onChange={(e) => {
							if (e.target.value == '') {
								changeSolo(NaN);
							} else {
							}
							adjustInputField(parseFloat(e.target.value), changeSolo);
						}}
						label='% Truck / Car'
						type='number'
						InputProps={{
							endAdornment: <InputAdornment position='end'>%</InputAdornment>,
						}}
						InputLabelProps={{
							shrink: true,
						}}
					/>
				</Grid>
			</Grid>
			<br />
			<br />
			<Paper>
				<Button
					disabled={props.loadingFlag}
					variant='contained'
					style={{ width: '100%' }}
					color={'secondary'}
					onClick={calculate(
						nofuel_transport,
						public_transport,
						solo_transport
					)}>
					{props.loadingFlag ? 'Calculating...' : 'Calculate'}
				</Button>
			</Paper>
		</div>
	);
}
