import Graph from '../components/Graph';
interface SimProps {
	refProp: any;
}
export default function Simulation(props: SimProps) {
	return (
		<div ref={props.refProp}>
			<Graph />
		</div>
	);
}
