import React from "react";
import { Box, Button, VStack, Text, Divider, Spinner } from "@chakra-ui/react";
import { Section } from "../types";

type Props = {
  structure: Section[];
  onSumarizar: (structure: Section[]) => void;
  isLoading: boolean;
  onBack: () => void;
};

export default function EstruturaView({ structure, onSumarizar, isLoading, onBack }: Props) {
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
      <Button colorScheme="blue" onClick={() => onSumarizar(structure)} isLoading={isLoading}>
        Organizar/Estruturar com IA
      </Button>
    </Box>
  );
}
