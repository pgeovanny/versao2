import React from "react";
import { Box, Button, VStack, Text, Divider } from "@chakra-ui/react";
import { Section } from "../types";

type Props = {
  structure: Section[];
  onEsquematizar: (structure: Section[]) => void;
  isLoading: boolean;
  onBack: () => void;
};

export default function EsquematizacaoView({ structure, onEsquematizar, isLoading, onBack }: Props) {
  return (
    <Box>
      <VStack align="stretch" spacing={4}>
        {structure.map((s, idx) => (
          <Box key={idx} bg="gray.50" p={4} rounded="md" boxShadow="sm">
            <Text fontWeight="bold">{s.title}</Text>
            <Text fontSize="sm">{s.content}</Text>
          </Box>
        ))}
      </VStack>
      <Divider my={6} />
      <Button variant="outline" mr={2} onClick={onBack}>
        Voltar
      </Button>
      <Button colorScheme="blue" onClick={() => onEsquematizar(structure)} isLoading={isLoading}>
        Esquematizar com IA
      </Button>
    </Box>
  );
}
