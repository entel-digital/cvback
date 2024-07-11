export const login = async () => {
  const path = "events";
  const body = {
    query: queries.allEvents,
  };
  const { data } = await Post(path, body);
  return data;
};
