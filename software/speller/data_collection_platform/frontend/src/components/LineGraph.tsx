import React from 'react';
import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

import ResponsiveChartWrapper from './ResponsiveChartWrapper';

const LineGraph = ({ data }: { data: any }) => {
  return (
    <ResponsiveChartWrapper style={{ margin: '0 8% 0 0' }}>
      {({ width, height }) => (
        <LineChart data={data} width={width} height={height}>
          <XAxis
            type="number"
            dataKey="name"
            domain={[0, 15]}
            tickCount={16}
            allowDataOverflow={true}
          />
          <YAxis type="number" domain={[0, 1]} yAxisId={0} />
          <YAxis type="number" yAxisId={1} />
          <YAxis type="number" yAxisId={2} />
          <Tooltip />
          <CartesianGrid stroke="#f5f5f5" />
          <Line type="monotone" dataKey="value" stroke="#ff7300" yAxisId={0} />
          <Line type="monotone" dataKey="diff" stroke="#088F8F" yAxisId={1} />
          <Line type="monotone" dataKey="int" stroke="#E6E6FA" yAxisId={2} />
        </LineChart>
      )}
    </ResponsiveChartWrapper>
  );
};

export default LineGraph;
