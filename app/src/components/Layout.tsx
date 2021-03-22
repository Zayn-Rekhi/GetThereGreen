import {
	Container,
	AppBar,
	Toolbar,
	Button,
	Grid,
	ThemeProvider,
} from '@material-ui/core';
import { mainTheme, colors } from '../theme';
import NavElem from './NavElem';
// import { Link } from 'react-router-dom';
// import NavWrap from './NavWrap';
import Logo from './LOGO.png';
import { makeStyles } from '@material-ui/core/styles';
interface LayoutProps {
	children: any;
	simclickHandle: any;
	topclickHandle: any;
	refProp: any;
}

export default function Layout(props: LayoutProps) {
	const useStyles = makeStyles((mainTheme) => ({
		root: {
			height: '200px',
			color: colors.white,
			width: '101vw',
			overflowX: 'hidden',
		},
		footer: {
			height: '75%',
			width: '102%',
		},
		subfoot: {
			backgroundColor: colors.blue,
			height: '40%',
			width: '100%',
		},
		link: {
			color: colors.white,
		},
	}));
	const classes = useStyles(mainTheme);
	return (
		<div style={{ overflowX: 'hidden' }} ref={props.refProp}>
			<ThemeProvider theme={mainTheme}>
				<AppBar>
					<Toolbar>
						{/* <NavWrap style={{ flex: 1 }} to='/'> */}
						<div style={{ flex: 1 }}>
							<img
								alt='Get There Green Logo'
								onClick={props.topclickHandle}
								height='80px'
								width='135px'
								src={Logo}
							/>
						</div>
						{/* <Typography>Get There Green</Typography> */}
						{/* </NavWrap> */}
						<NavElem onClick={props.simclickHandle}>Simulation</NavElem>
						<NavElem onClick={props.topclickHandle}>About</NavElem>
					</Toolbar>
				</AppBar>
				<br /> {/* haha webdev go brr */}
				<br />
				<br />
				<br />
				<br />
				<Container>{props.children}</Container>
				<br />
				<br />
				<br />
				<br />
				<br />
				<br />
				<div className={classes.root}>
					<Grid className={classes.footer} container spacing={3}></Grid>
					<Grid className={classes.subfoot} container>
						<div style={{ display: 'inline-block', margin: 'auto' }}>
							<a
								rel='noreferrer'
								href='https://github.com/Zayn-Rekhi/GetThereGreen'
								target='_blank'>
								<Button style={{ padding: '20px' }} color='primary'>
									By Zayn Rekhi and Joey Sorkin
								</Button>
							</a>
						</div>
					</Grid>
				</div>
			</ThemeProvider>
		</div>
	);
}
