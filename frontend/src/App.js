import './App.css';
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";
import Banks from './components/Banks';
import Dashboard from './components/Dashboard';
import Requests from './components/Requests';
import 'bootstrap/dist/css/bootstrap.min.css';
function App() {
  return (
    <Router>
      <div className="App">
        <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
            <ul className="navbar-nav ml-auto">
              <li><Link to={'/'} className="nav-link"> Banks </Link></li>
              <li><Link to={'/requests'} className="nav-link">Requests</Link></li>
              <li><Link to={'/dashboard'} className="nav-link">Dashboard</Link></li>
            </ul>
            </nav>
            <Switch>
                <Route exact path='/' component={Banks} />
                <Route path='/requests' exact component={Requests} />
                <Route path='/dashboard' exact component={Dashboard} />
            </Switch>
      </div>
    </Router>
  );
}

export default App;
