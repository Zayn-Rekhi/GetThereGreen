import Typography from '@material-ui/core/Typography';
import TextBlock from '../components/TextBlock';

export default function About() {
	return (
		<div>
			<Typography variant='h1'>Get There Green</Typography>
			<Typography variant='h4'>
				<i>
					A project that displays how your commute affects the quality of the
					air around you
				</i>
				<hr />
			</Typography>
			<br />
			<TextBlock title='The Problem:'>
				Since rapid industrialization took place, the quality of air around us
				rapidly decreased. The burning of fossil fuels and production of various
				forms of energy lead to more pollutants being released into the
				atmosphere to a nearly toxic point. Efforts to drastically decrease air
				pollution is often seen as the responsibility of large companies, which
				leaves most people with very little they can do to help decrease air
				pollution.
			</TextBlock>

			<TextBlock title="Let's Change That:">
				Almost everyday of the week, around 143 million Americans wake up and
				begin their commute. There are various means of transportation used to
				get people to work such as a trains, busses, cars and bikes. Analyzing
				commute data from the US Census and comparing it to air pollution data
				from the last 10 years allows us to find the impact your commute vehicle
				has on the quality of the air around you. This is the idea behind Get
				There Green, an interactive simulation that predicts the air quality for
				the next 10 years based off of custom commuter statistics
			</TextBlock>
			<TextBlock title='How It Works:'>
				Get There Green is powered by a neural network. A neural network is a
				program that can be "trained" on past data and effects in order to
				predict future effects given new data. In our case, we trained it on
				past{' '}
				<a href='https://data.census.gov/cedsci/table?q=ACSDT1Y2019.B08301&g=0100000US.050000&tid=ACSDT1Y2019.B08301&moe=true&hidePreview=true'>
					US Census
				</a>{' '}
				data regarding the means of transportation used in peoples commute to
				work, and compared it to the{' '}
				<a href='https://aqs.epa.gov/aqsweb/airdata/download_files.html#Daily'>
					data on various air pollutants
				</a>{' '}
				in the years reflecting the census data. After some fine tuning,
				predictions begin to look relatively accurate.
			</TextBlock>
			{/* <Simulation /> */}
		</div>
	);
}
