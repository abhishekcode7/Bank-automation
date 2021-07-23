import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import {Button} from 'react-bootstrap'
const useStyles = makeStyles({
    table: {
      minWidth: 650,
    },
  });
  
  function createData(bank , cash , approve , reject ) {
    return { bank,cash,approve,reject };
  }
  
  const rows = [
    createData('ICICI', 159,<Button variant="outline-success">Approve</Button>,<Button variant="outline-danger">Reject</Button>),
    createData('SBI', 237, <Button variant="outline-success">Approve</Button>,<Button variant="outline-danger">Reject</Button>),
    createData('AXIS', 262, <Button variant="outline-success">Approve</Button>,<Button variant="outline-danger">Reject</Button>)
  ];

const Requests = () =>{
    const classes = useStyles();
    return(
        <div>
        <div>
        <TableContainer component={Paper}>
            <Table className={classes.table} aria-label="simple table">
                <TableHead>
                <TableRow>
                    <TableCell>Bank</TableCell>
                    <TableCell align="right">Cash Recieved</TableCell>
                    <TableCell align="right">Action</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {rows.map((row) => (
                    <TableRow key={row.name}>
                    <TableCell component="th" scope="row">
                        {row.bank}
                    </TableCell>
                    <TableCell align="right">{row.cash}</TableCell>
                    <TableCell align="right">{row.approve}{row.reject}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
            </TableContainer>
            
        </div>
    </div> 
    )
}
export default Requests;