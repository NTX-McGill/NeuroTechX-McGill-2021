const query = async (endpoint: string, method: string, data: object = {}) => {
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
//
// prettier-ignore
const api = {
  anxiousStart: (d: { time: string }) =>
    query("/api/anxious/start", "POST", d),

  anxiousStop: (d: { time: string }) =>
    query("/api/anxious/stop", "POST", d),

  sendFeedback: (d: { url: string; stress_level: 1 | 2 | 3 }) =>
    query("/api/feedback", "POST", d),
};
export default api;
