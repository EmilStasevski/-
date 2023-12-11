import {
  BarChart,
  Title,
  Bar,
  Tooltip,
  CartesianGrid,
  Legend,
  XAxis,
  YAxis,
} from "recharts";

export default function BarChartApproval(props) {
  let plotData = props.SelectedConstRFRegion;
  console.log(plotData);
  return (
    <>
      <h3>Голоса за </h3>
      <BarChart
        title="Президентские выборы"
        width={500}
        height={250}
        data={plotData}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <Bar dataKey="pro_votes_number" fill="blue" />

        <YAxis />
        <Tooltip />
        <Legend />
        <Title text="v sjn osnspi" />
      </BarChart>
    </>
  );
}
