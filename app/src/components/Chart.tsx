import {
	VictoryLine,
	VictoryChart,
	VictoryAxis,
	VictoryTheme,
	VictoryLegend,
} from 'victory';
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
interface ChartProps {
	max: number;
	data: DataIN;
}
export default function Chart(props: ChartProps) {
	return (
		<div>
			<VictoryChart
				domain={{ x: [0, 10], y: [0, props.max] }}
				height={400}
				width={1000}
				animate={{
					duration: 500,
					onLoad: { duration: 500 },
				}}
				domainPadding={20}
				theme={VictoryTheme.material}>
				<VictoryAxis
					tickValues={Array.from(
						{ length: props.max },
						(_, i) => (i + 1) * (props.max > 100 ? 100 : 10)
					)}
					dependentAxis={true}
					style={{
						grid: { stroke: 'grey' },
						axisLabel: { fontSize: 20, padding: 30 },
					}}
					label='Amount (ppb)'
				/>
				<VictoryAxis />
				<VictoryAxis
					tickValues={Array.from({ length: 9 }, (_, i) => i + 1)}
					style={{
						grid: { stroke: 'grey' },
						axisLabel: { fontSize: 20, padding: 26 },
					}}
					label='Time (years in the future)'
				/>
				<VictoryAxis />
				<VictoryLegend
					x={500}
					y={0}
					orientation='horizontal'
					gutter={20}
					style={{
						border: { stroke: 'black' },
						title: { fontSize: 10 },
					}}
					data={[
						{ name: 'Ozone', symbol: { fill: 'blue' } },
						{ name: 'Sulfur Dioxide', symbol: { fill: 'orange' } },
						{ name: 'Nitrogen Dioxide', symbol: { fill: 'green' } },
						{ name: 'Carbon Monoxide', symbol: { fill: 'gray' } },
					]}
				/>
				<VictoryLine
					style={{
						data: {
							stroke: 'blue',
						},
					}}
					interpolation='natural'
					data={props.data.Ozone}
					x='x'
					y='y'
				/>
				<VictoryLine
					style={{
						data: {
							stroke: 'orange',
						},
					}}
					interpolation='natural'
					data={props.data.SulfurDioxide}
					x='x'
					y='y'
				/>
				<VictoryLine
					style={{
						data: {
							stroke: 'gray',
						},
					}}
					interpolation='natural'
					data={props.data.CarbonMonoxide}
					x='x'
					y='y'
				/>
				<VictoryLine
					style={{
						data: {
							stroke: 'green',
						},
					}}
					interpolation='natural'
					data={props.data.NitrogenDioxide}
					x='x'
					y='y'
				/>
			</VictoryChart>
		</div>
	);
}
