import SelectYear from "./SelectYear";
import Papa from "papaparse";

import React, { Suspense, useEffect, useState } from "react";
import PresidentBarChart from "./PresidentBarChart";

import { db } from "../../FirebaseConfig";
import { onValue, ref } from "firebase/database";

export default function PresidentInfo(props) {
  const [projects, setProjects] = useState([]);
  useEffect(() => {
    const query = ref(db, "PresidentElection");
    return onValue(query, (snapshot) => {
      const data = snapshot.val();

      if (snapshot.exists()) {
        Object.values(data).map((project) => {
          setProjects((projects) => [...projects, project]);
        });
      }
    });
  }, []);
  let SelectedPredisentElection = projects.filter(
    (element) => element.year === props.SelectedYear
  );

  return (
    <>
      <h2>Выборы президента РФ в {props.SelectedYear} году</h2>
      <PresidentBarChart
        SelectedPredisentElection={SelectedPredisentElection}
      />
    </>
  );
}
