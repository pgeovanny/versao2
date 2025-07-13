import React from "react";
import { Box, Button, VStack, Text, Divider } from "@chakra-ui/react";
import { Section } from "../types";

interface Props {
  structure: Section[];
  onSumarizar: (structure: Section[]) => void;
  isLoading: boolean;
  onBack: () => void;
}

const EstruturaView: React.FC<Props> = ({ structure, onSumarizar, isLoading, onBack }) => (
  <Box>
    <VStack align="stretch" spacing={2} mb={4}>
      <Text fontWeight="bold">Prévia da estrutura extraída:</Text>
      <Box maxH="300px" overflowY="auto" borderWidth={1} borderRadius="md" p={2}>
        {structure.map((sec, idx) => (
          <Box key={idx} mb={2}>
            <Text fontWeight="semibold">{sec.title}</Text>
            <Text fontSize="sm" color="gray.700">{sec.content.slice(0, 350)}...</Text>
            <Divider my={2} />
          </Box>
        ))}
      </Box>
    </VStack>
    <Button colorScheme="blue" onClick={() => onSumarizar(structure)} isLoading={isLoading} mr={2}>
      Organizar Estrutura (IA)
    </Button>
    <Button onClick={onBack} variant="ghost">
      Voltar
    </Button>
  </Box>
);

export default EstruturaView;
