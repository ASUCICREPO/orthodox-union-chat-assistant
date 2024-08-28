import React from "react";
import Grid from "@mui/material/Grid";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { useLanguage } from "../utilities/LanguageContext"; // Adjust the import path
import { ABOUT_US_HEADER_BACKGROUND, ABOUT_US_TEXT, FAQ_HEADER_BACKGROUND, FAQ_TEXT, TEXT, FIRST_WORD_COLOR } from "../utilities/constants"; // Adjust the import path
import closeIcon from "../Assets/close.svg"; // Assuming close.svg is an image
import arrowRightIcon from "../Assets/arrow_right.svg"; // Assuming arrow_right.svg is an image

function LeftNav({ showLeftNav = true, setLeftNav }) {
  const { language } = useLanguage();

  return (
    <>
      <Grid className="appHeight100">
        <Grid container direction="column" justifyContent="flex-start" alignItems="stretch" padding={4} spacing={2}>
          {showLeftNav ? (
            <>
              <Grid item container direction="column" justifyContent="flex-start" alignItems="flex-end">
                <img
                  src={closeIcon}
                  alt="Close Panel"
                  onClick={() => setLeftNav(false)} // Removed extra parentheses
                />
              </Grid>
              <Grid item>
                <Typography variant="h6" sx={{ fontWeight: "bold" }}>
                  <Box component="span" sx={{ color: FIRST_WORD_COLOR }}>
                    {TEXT[language].ABOUT_US_TITLE.split(' ')[0]}
                  </Box>{' '}
                  <Box component="span" sx={{ color: ABOUT_US_HEADER_BACKGROUND }}>
                    {TEXT[language].ABOUT_US_TITLE.split(' ').slice(1).join(' ')}
                  </Box>
                </Typography>
              </Grid>
              <Grid item>
                <Typography variant="subtitle1" color={ABOUT_US_TEXT} paragraph>
                  {TEXT[language].ABOUT_US.split('\n\n')[0]}
                </Typography>
                <Typography variant="subtitle1" color={ABOUT_US_TEXT}>
                  {TEXT[language].ABOUT_US.split('\n\n')[1]}
                </Typography>
              </Grid>
              {/* <Grid item>
                <Typography variant="h6" sx={{fontWeight:"bold"}} color={FAQ_HEADER_BACKGROUND}>{TEXT[language].FAQ_TITLE}</Typography>
              </Grid> */}
              {/* <Grid item>
                <ul >
                  {TEXT[language].FAQS.map((question, index) => (
                    <li key={index} >
                      <Typography variant="subtitle1" color={FAQ_TEXT}>{question}</Typography>
                    </li>
                  ))}
                </ul>
              </Grid> */}
            </>
          ) : (
            <>
              <Grid item container direction="column" justifyContent="flex-start" alignItems="flex-end">
                <img
                  src={arrowRightIcon}
                  alt="Open Panel"
                  onClick={() => setLeftNav(true)} // Removed extra parentheses
                />
              </Grid>
            </>
          )}
        </Grid>
      </Grid>
    </>
  );
}

export default LeftNav;
