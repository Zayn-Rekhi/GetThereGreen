import React from 'react';
import Typography from '@material-ui/core/Typography';
interface TextBlockProps {
	title: string;
	children: any;
}
export default function TextBlock(props: TextBlockProps) {
	return (
		<>
			<br />
			<Typography variant='h2'>{props.title}</Typography>
			<br />
			<Typography variant='body1'>{props.children}</Typography>
			<br />
		</>
	);
}
