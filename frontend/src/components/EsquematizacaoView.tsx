import React from "react";
import { Box, Button, VStack, Text, Divider } from "@chakra-ui/react";
import { Section } from "../types";

interface Props {
  structure: Section[];
  onEsquematizar: (structure: Section[]) => void;
  isLoading: boolean;
  onBack: () => void;
}

const EsquematizacaoView: React.FC<Props> = ({ structure, onEsquematizar, isLoading, onBack }) => (
  <Box>
    <VStack align="stretch" spacing={2} mb={4}>
      <Text fontWeight="bold">Estrutura organizada. Pronto para esquematizar a Lei:</Text>
      <Box maxH="300px" overflowY="auto" borderWidth={1} borderRadius="md" p={2}>
        {structure.map((sec, idx) => (
          <Box key={idx} mb={2}>
            <Text fontWeight="semibold">{sec.title}</Text>
            <Text fontSize="sm" color="gray.600">{sec.content.slice(0, 350)}...</Text>
            <Divider my={2} />
          </Box>
        ))}
      </Box>
    </VStack>
    <Button colorScheme="blue" onClick={() => onEsquematizar(structure)} isLoading={isLoading} mr={2}>
      Esquematizar com IA
    </Button>
    <Button onClick={onBack} variant="ghost">
      Voltar
    </Button>
  </Box>
);

export default EsquematizacaoView;
