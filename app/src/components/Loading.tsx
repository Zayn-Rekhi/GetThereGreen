import React from 'react';
import LinearProgress from '@material-ui/core/LinearProgress';
import Typography from '@material-ui/core/Typography';
interface LoadingProps {
	visibility: boolean;
}
export default function Loading(props: LoadingProps) {
	if (props.visibility) {
		return (
			<div style={{ textAlign: 'center' }}>
				<LinearProgress />
				<Typography variant='body1'>
					Your request is being processed. Machine learning is complex, so this
					may take up to 20 seconds
				</Typography>
				<LinearProgress />
				<br />
			</div>
		);
	} else {
		return <div></div>;
	}
}
