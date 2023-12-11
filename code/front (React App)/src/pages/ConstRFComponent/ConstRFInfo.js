import SelectRegion from "./SelectRegion";
import React, { Suspense, useEffect, useState } from "react";

import { db } from "../../FirebaseConfig";
import { onValue, ref } from "firebase/database";
import BarChartApproval from "./BarChartApproval";

export default function ConstRFInfo(props) {
  const [projects, setProjects] = useState([]);
  useEffect(() => {
    const query = ref(db, "ConstRF");
    return onValue(query, (snapshot) => {
      const data = snapshot.val();

      if (snapshot.exists()) {
        Object.values(data).map((project) => {
          setProjects((projects) => [...projects, project]);
        });
      }
    });
  }, []);

  let SelectedConstRFRegion = projects.filter(
    (element) => element.region === props.SelectedRegion
  );
  console.log(Object.keys(projects).length);

  return (
    <>
      <h4>Голосования по поправкам в Конституцию по {props.SelectedRegion} </h4>
      <BarChartApproval SelectedConstRFRegion={SelectedConstRFRegion} />
    </>
  );
}
