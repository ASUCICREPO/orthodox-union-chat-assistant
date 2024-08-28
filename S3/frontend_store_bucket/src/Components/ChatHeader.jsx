import React from "react";
import Typography from "@mui/material/Typography";
import Box from "@mui/material/Box";
import { useLanguage } from "../utilities/LanguageContext"; // Adjust the import path
import { TEXT, HEADER_TEXT_GRADIENT, FIRST_WORD_COLOR } from "../utilities/constants"; // Adjust the import path
import { Container } from "@mui/material";

function ChatHeader({ selectedLanguage }) {
  const { language: contextLanguage } = useLanguage();
  const language = selectedLanguage || contextLanguage || 'EN'; // Use selectedLanguage if provided, otherwise default to contextLanguage or 'EN'

  return (
    <Container
      sx={{
        display: 'flex',
        justifyContent: 'left',
        alignItems: 'center',
        height: '100%',
      }}
    >
      <Typography variant="h4" className="chatHeaderText" sx={{ textAlign: 'left', fontSize: "2.5rem"}}>
        <Box 
          component="span" 
          sx={{ 
            background: FIRST_WORD_COLOR,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}
        >
          {(TEXT[language]?.CHAT_HEADER_TITLE || "Default Chat Header Title").split(' ')[0]}
        </Box>{' '}
        <Box 
          component="span" 
          sx={{ 
            background: HEADER_TEXT_GRADIENT,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}
        >
          {(TEXT[language]?.CHAT_HEADER_TITLE || "Default Chat Header Title").split(' ').slice(1).join(' ')}
        </Box>
      </Typography>
    </Container>
  );
}

export default ChatHeader;
