import { createMuiTheme, responsiveFontSizes } from '@material-ui/core/styles';
const colors = {
	blue: '#225271',
	green: '#0F978E',
	mint: '#78CC97',
	white: '#E9EBED',
};

const mainThemebase = createMuiTheme({
	palette: {
		common: {
			black: colors.blue,
			white: colors.white,
		},
		primary: {
			main: colors.mint,
		},
		secondary: {
			main: colors.blue,
		},
		background: {
			default: colors.white,
		},
	},
	overrides: {},
	typography: {
		body1: {
			fontFamily: 'Merriweather, serif',
			lineHeight: '30px',
			fontSize: '16px',
		},
		button: {
			fontFamily: 'Source Sans Pro, sans-serif',
		},
		h1: {
			fontFamily: 'Source Sans Pro, sans-serif',
		},
		h2: {
			fontFamily: 'Source Sans Pro, sans-serif',
			// fontSize: '20px',
		},
		h4: {
			fontFamily: 'Merriweather, serif',
			// fontSize: '20px',
		},
	},
});
const mainTheme = responsiveFontSizes(mainThemebase);
export { mainTheme, colors };
