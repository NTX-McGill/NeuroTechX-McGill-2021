import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import useResizeObserver from 'use-resize-observer';

const useStyles = makeStyles(theme => ({
  responsiveChart: {
    'flex': 1,
    'minWidth': 0,
    'minHeight': 0,
    'display': 'flex',
    'justifyContent': 'center',
    'alignItems': 'center',

    '& svg': {
      overflow: 'visible',
    },
  },
}));

interface ResponsiveChartWrapperProps
  extends React.HTMLAttributes<HTMLDivElement> {
  children: React.FunctionComponent<{ width: number; height: number }>;
}

const ResponsiveChartWrapper = ({
  children,
  ...rest
}: ResponsiveChartWrapperProps) => {
  const classes = useStyles();
  const {
    ref: containerRef,
    width = 0,
    height = 0,
  } = useResizeObserver<HTMLDivElement>();

  return (
    <div
      {...rest}
      className={`${classes.responsiveChart} ${rest.className ?? ''}`}
      ref={containerRef}
    >
      {Math.min(width, height) > 0 && children({ width, height })}
    </div>
  );
};

export default ResponsiveChartWrapper;
