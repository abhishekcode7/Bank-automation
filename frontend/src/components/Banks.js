import { useState, useEffect } from "react";
import { Image } from "react-bootstrap";
import "./Banks.css";
import sample from "../images/sample.png";
import React from "react";
import sbi from "../images/sbi.png";
import axios from "axios";
import { TextField, Button, Box } from "@material-ui/core";
import Login from "./Login";
import { IoLogInOutline } from "react-icons/io5";
import { FiEdit } from "react-icons/fi";
const Banks = () => {
  const [captcha, setCap] = useState("");
  const [capImg, setImg] = useState("Getting captcha ...");
  const [sbiStatus, setSbiStatus] = useState(0);
  const [iciStatus, setIciStatus] = useState(0);
  const [otp, setOtp] = useState(0);
  const [logStart, setLogStart] = useState(0);
  const [showCap, setShowCap] = useState(0);
  const [otpButton, setOtpButton] = useState(0);
  const [loop, setLoop] = useState(0);
  const [userSetting, setUserSetting] = useState(0);

  const styleCard = {
    maxWidth: "210px",
  };
  useEffect(() => {
    setTimeout(() => {
      fetch("/api/status")
        .then((res) => res.json())
        .then((data) => {
          if (data.st === "1") {
            setSbiStatus(1);
            setOtpButton(0);
            setShowCap(0);
            setLogStart(0);
          } else setSbiStatus(0);
        });
      fetch("/api/checkCaptcha")
        .then((res) => res.json())
        .then((data) => {
          if (data.image !== "0") {
            setImg(data.image.substring(2, data.image.length - 1));
            setShowCap(1);
          }
        });
      setLoop((loop + 1) % 10);
    }, 1000);
  }, [loop]);
  let runScript = (e) => {
    e.preventDefault();
    setLogStart(1);
    setUserSetting(0);
    fetch("/api/runScript")
      .then((res) => res.json())
      .then((data) => {
        if (data.code === "0") {
          setLogStart(0);
          setShowCap(0);
          alert(
            "Please Update Bank Details (Invalid Credentials) . One or both Id / Pass is null field"
          );
        }
      })
      .catch((err) => {
        alert("Login failed ! Please Try Again ");
      });
  };
  let submitCap = (e) => {
    e.preventDefault();
    const send = { cap: captcha };
    axios
      .post("/api/submitCaptcha", send)
      .then((res) => {
        if (res.data.code === "0") {
          setLogStart(0);
          setOtpButton(0);
          setShowCap(0);
          alert(
            " You entered wrong Captcha or Invalid Credentials , Please login again "
          );
        } else setOtpButton(1);
      })
      .catch((err) => console.log(err));
  };
  let submitOTP = (e) => {
    e.preventDefault();
    const send = { OTP: otp };
    axios
      .post("/api/submitOtp", send)
      .then((res) => {
        if (res.data.code === "0") {
          setLogStart(0);
          setOtpButton(0);
          setShowCap(0);
          alert(" You entered wrong OTP , Please login again ");
        } else {
          axios.post("/api/loop3", send).then(res);
        }
      })
      .catch((err) => console.log(err));
  };
  return (
    <div>
      <div className="Bank-container">
        <div className="card mb-4 h-25" style={styleCard}>
          <div className="row no-gutters">
            <div className="col-md-2 text-center mx-auto d-flex align-items-center">
              <img src={sbi} className="card-img" alt="..." />
            </div>
            <div className="col-md-9">
              <div className="card-body">
                <h5 className="card-title">SBI </h5>
                {sbiStatus === 1 ? (
                  <p className="card-text" style={{ color: "green" }}>
                    Logged In
                  </p>
                ) : (
                  <p className="card-text" style={{ color: "red" }}>
                    Session Out
                  </p>
                )}

                <div className="card-edits">
                  <h4>
                    <FiEdit
                      title="Edit Bank Details"
                      onClick={() => {
                        userSetting === 1
                          ? setUserSetting(0)
                          : setUserSetting(1);
                      }}
                    />
                  </h4>
                  {sbiStatus === 1 || showCap === 1 || otpButton === 1 ? (
                    ""
                  ) : (
                    <h2>
                      <IoLogInOutline title="Login" onClick={runScript} />
                    </h2>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="card mb-4 h-25" style={styleCard}>
          <div className="row no-gutters">
            <div className="col-md-2 text-center mx-auto d-flex align-items-center">
              <img src={sample} className="card-img" alt="..." />
            </div>
            <div className="col-md-9">
              <div className="card-body">
                <h5 className="card-title">ICICI</h5>
                {sbiStatus === 1 ? (
                  <p className="card-text" style={{ color: "green" }}>
                    Logged In
                  </p>
                ) : (
                  <p className="card-text" style={{ color: "red" }}>
                    Session Out
                  </p>
                )}

                <div className="card-edits">
                  <h4>
                    <FiEdit
                      title="Edit Bank Details"
                      onClick={() => setUserSetting(1)}
                    />
                  </h4>
                  {sbiStatus === 1 || showCap === 1 || otpButton === 1 ? (
                    ""
                  ) : (
                    <h2>
                      <IoLogInOutline title="Login" onClick={runScript} />
                    </h2>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      {userSetting === 1 ? <Login /> : ""}
      <div className="text-center">
        {logStart === 1 && showCap === 0 && otpButton === 0 ? (
          <div>Getting captcha</div>
        ) : (
          ""
        )}
        {showCap === 1 && otpButton === 0 ? (
          <Image
            className="captcha"
            src={`data:image/png;base64,${capImg}`}
            style={{ width: "10rem" }}
            rounded
          />
        ) : (
          ""
        )}
      </div>
      <form>
        {showCap === 1 && otpButton === 0 ? (
          <Box
            display="flex"
            // width={500}
            height={80}
            alignItems="center"
            justifyContent="center"
          >
            <TextField
              id="outlined-basic"
              label="Enter Captcha"
              variant="outlined"
              size="small"
              onChange={(event) => setCap(event.target.value)}
            />
            <Button
              variant="contained"
              color="primary"
              size="medium"
              style={{ marginLeft: "10px" }}
              onClick={submitCap}
            >
              Submit
            </Button>
          </Box>
        ) : (
          ""
        )}
        {otpButton === 1 ? (
          <Box
            display="flex"
            // width={500}
            height={80}
            alignItems="center"
            justifyContent="center"
          >
            <TextField
              id="outlined-basic"
              label="Enter OTP"
              variant="outlined"
              size="small"
              onChange={(event) => setOtp(event.target.value)}
            />
            <Button
              variant="contained"
              color="primary"
              size="medium"
              style={{ marginLeft: "10px" }}
              onClick={submitOTP}
            >
              Submit
            </Button>
          </Box>
        ) : (
          ""
        )}
      </form>
    </div>
  );
};
export default Banks;
