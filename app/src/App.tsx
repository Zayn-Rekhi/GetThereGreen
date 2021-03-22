import React from 'react';
import Layout from './components/Layout';
import About from './pages/About';
import Simulation from './pages/Simulation';
function App() {
	const simref = React.useRef(null);
	const topref = React.useRef(null);
	const handleTopClick = () =>
		//@ts-ignore
		topref.current.scrollIntoView({
			behavior: 'smooth',
			block: 'start',
		});
	const handleSimClick = () =>
		//@ts-ignore
		simref.current.scrollIntoView({
			behavior: 'smooth',
			block: 'start',
		});
	return (
		<div className='App'>
			<Layout
				refProp={topref}
				topclickHandle={handleTopClick}
				simclickHandle={handleSimClick}>
				<About />
				<Simulation refProp={simref} />

				{/* <Route path='/sim'>
							<Users />
						</Route>
						<Route path='/'>
							<Home />
						</Route> */}
			</Layout>
		</div>
	);
}

export default App;
