import React from 'react';
import { Button } from '@material-ui/core';
interface NavElemProps {
	children: String;
	onClick: any;
}
export default function NavElem(props: NavElemProps) {
	return (
		<Button onClick={props.onClick} style={{ padding: '20px' }}>
			{props.children}
		</Button>
	);
}
