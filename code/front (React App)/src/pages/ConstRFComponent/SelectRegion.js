import React from "react";
import Select from "react-select";
import { useState } from "react";
import ConstRFInfo from "./ConstRFInfo";

export default function SelectRegion(props) {
  let [userChoice, setUserChoice] = useState("Республика Адыгея (Адыгея)");
  const options = [
    { label: "Республика Адыгея (Адыгея)", id: 2 },
    { label: "Республика Татарстан", id: 3 },
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
      <ConstRFInfo SelectedRegion={userChoice} />
    </>
  );
}
