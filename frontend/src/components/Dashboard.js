import { useState } from "react";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import "./Dashboard.css";
// import { PieChart } from 'react-minimal-pie-chart';
import { makeStyles } from "@material-ui/core/styles";
import Table from "@material-ui/core/Table";
import TableBody from "@material-ui/core/TableBody";
import TableCell from "@material-ui/core/TableCell";
import TableContainer from "@material-ui/core/TableContainer";
import TableHead from "@material-ui/core/TableHead";
import TableRow from "@material-ui/core/TableRow";
import Paper from "@material-ui/core/Paper";
import axios from "axios";

const useStyles = makeStyles({
  table: {
    minWidth: 650,
  },
});

function createData(bank, cash, fund) {
  return { bank, cash, fund };
}
let rows = [
  createData("SBI", 4525, 6),
  createData("ICICI", 237, 9),
  createData("AXIS", 262, 16),
];
const Dashboard = () => {
  const [startDate, setStartDate] = useState(new Date());
  const [sbiMoney, setSbiMoney] = useState(0);
  const classes = useStyles();
  const updateDash = (e) => {
    e.preventDefault();
    let s = String(startDate);
    // Wed Jun 09 2021
    const send = {
      Month: s.substr(4, 3),
      Date: s.substr(8, 2),
      Year: s.substr(11, 4),
    };
    axios
      .post("/api/getDashboard", send)
      .then((res) => {
        setSbiMoney(res.data.code);
      })
      .catch((err) => console.log(err));
  };
  return (
    <div>
      <div className="date-container">
        <div>Select date to get analytics of that day : </div>
        <DatePicker
          className="date-selected"
          selected={startDate}
          onChange={(date) => setStartDate(date)}
        />
        <button
          type="button"
          className="btn btn-info fetch-data"
          onClick={updateDash}
        >
          Get data
        </button>
      </div>
      <div>
        <TableContainer component={Paper}>
          <Table className={classes.table} aria-label="simple table">
            <TableHead>
              <TableRow>
                <TableCell>Bank</TableCell>
                <TableCell align="right">Cash Recieved</TableCell>
                <TableCell align="right">Fund Approved</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {/* {rows.map((row) => (
                <TableRow key={row.name}>
                  <TableCell component="th" scope="row">
                    {row.bank}
                  </TableCell>
                  <TableCell align="right">{row.cash}</TableCell>
                  <TableCell align="right">{row.fund}</TableCell>
                </TableRow>
              ))} */}
              <TableRow key={rows[0].bank}>
                <TableCell component="th" scope="row">
                  {rows[0].bank}
                </TableCell>
                <TableCell align="right">{sbiMoney}</TableCell>
                <TableCell align="right">{rows[0].fund}</TableCell>
              </TableRow>
              <TableRow key={rows[1].bank}>
                <TableCell component="th" scope="row">
                  {rows[1].bank}
                </TableCell>
                <TableCell align="right">{rows[1].cash}</TableCell>
                <TableCell align="right">{rows[1].fund}</TableCell>
              </TableRow>
              <TableRow key={rows[2].bank}>
                <TableCell component="th" scope="row">
                  {rows[2].bank}
                </TableCell>
                <TableCell align="right">{rows[1].cash}</TableCell>
                <TableCell align="right">{rows[2].fund}</TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </TableContainer>
        <div>
          {/* <PieChart
                    data={[
                    { title: 'One', value: 10, color: '#E38627' },
                    { title: 'Two', value: 15, color: '#C13C37' },
                    { title: 'Three', value: 20, color: '#6A2135' },
                    ]} 
                    radius="10" center={[50,14] animate=true }
                        /> */}
        </div>
      </div>
    </div>
  );
};
export default Dashboard;
