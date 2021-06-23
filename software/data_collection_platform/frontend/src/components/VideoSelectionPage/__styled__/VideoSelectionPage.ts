import styled from "styled-components";

export const ThumbnailContainer = styled.div`
  display: flex;
  margin: 10px 0;

  img {
    max-width: 250px;
    max-height: 250px;
    border-radius: 5px;
  }

  .MuiCheckbox-root {
    color: var(--color-primary-blue);

    svg {
      color: var(--color-primary-blue);
    }
  }
`;

export const InfoContainer = styled.div`
  display: flex;
  flex-direction: column;
  color: var(--color-primary-blue);

  p {
    margin-left: 30px;
  }
`;

export const VideoSelectionContainer = styled.div`
  height: 80%;
  overflow-y: auto;
`;

export const SelectionPageContainer = styled.div`
  h1 {
    padding: 20px 0;
  }
  padding: 50px;
  height: 80vh;
`;
