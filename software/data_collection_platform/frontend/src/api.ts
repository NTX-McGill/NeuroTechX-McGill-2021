const endpoints = {
  // {
  //   time: string; // RFC3339 time
  // }
  anxiousStart: {
    method: "POST",
    endpoint: "/api/anxious/start",
  },

  // {
  //   time: string // RFC3339 time
  // }
  anxiousStop: {
    method: "POST",
    endpoint: "/api/anxious/stop",
  },
};

type Endpoints = typeof endpoints;

type Api = {
  [k in keyof Endpoints]: (
    data: object,
  ) => ReturnType<ReturnType<typeof makeQuery>>;
};

const makeQuery = ({ endpoint, method }: Endpoints[keyof Endpoints]) => async (
  data: object = {},
) => {
  if (process.env.REACT_APP_SERVER_URL === undefined)
    throw new Error("$REACT_APP_SERVER_URL is undefined");
  const url = `${process.env.REACT_APP_SERVER_URL}${endpoint}`;

  const resp = await fetch(url, {
    method,
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });
  return resp.json();
};

// Constructs an Api object that we can use to call the endpoints
// specified above.
//
// e.g.
//   api.anxietyUp({ ... })
//   api.anxietyDown({ ... })
const api = Object.fromEntries(
  Object.entries(endpoints).map(([k, v]) => [k, makeQuery(v)]),
) as Api;
export default api;
