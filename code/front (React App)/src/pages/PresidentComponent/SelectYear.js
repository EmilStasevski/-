import React from "react";
import Select from "react-select";
import { useState } from "react";
import PresidentInfo from "./PresidentInfo";

export default function SelectYear(props) {
  let [userChoice, setUserChoice] = useState("2018");
  const options = [
    // { label: "2004", id: 0 },
    // { label: "2008", id: 1 },
    { label: "2012", id: 2 },
    { label: "2018", id: 3 },
  ];
  return (
    <>
      <div className="SelectBox">
        <Select
          className="CountryYear"
          options={options}
          onChange={(choice) => setUserChoice(choice.label)}
        />
      </div>
      <PresidentInfo SelectedYear={userChoice} />
    </>
  );
}
