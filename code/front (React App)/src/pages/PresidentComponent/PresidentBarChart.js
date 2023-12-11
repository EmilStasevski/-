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

export default function PresidentBarChart(props) {
  let plotData = props.SelectedPredisentElection;
  console.log(plotData);
  return (
    <>
      <h3>Общее распределение голосов </h3>
      <BarChart
        title="Президентские выборы"
        width={500}
        height={250}
        data={plotData}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <Bar dataKey="percentage" fill="blue" />

        <XAxis dataKey="candidate" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Title text="v sjn osnspi" />
      </BarChart>
    </>
  );
}
