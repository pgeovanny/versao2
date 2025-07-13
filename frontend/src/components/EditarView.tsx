import React from "react";
import { Box, Button, VStack, Text, Textarea, Divider } from "@chakra-ui/react";
import { Section, SchematizedSection } from "../types";

type Props = {
  structure: Section[];
  schematization: SchematizedSection[];
  onEditar: (args: { structure: Section[]; schematization: SchematizedSection[] }) => void;
  isLoading: boolean;
  onBack: () => void;
};

export default function EditarView({
  structure,
  schematization,
  onEditar,
  isLoading,
  onBack,
}: Props) {
  // Você pode adicionar lógica de edição aqui!
  // Por enquanto, só mostra o texto gerado.

  return (
    <Box>
      <VStack align="stretch" spacing={4}>
        {schematization.map((s, idx) => (
          <Box key={idx} bg="gray.50" p={4} rounded="md" boxShadow="sm">
            <Text fontWeight="bold">{s.title}</Text>
            <Textarea isReadOnly minH="120px" value={s.schematization} />
          </Box>
        ))}
      </VStack>
      <Divider my={6} />
      <Button variant="outline" mr={2} onClick={onBack}>
        Voltar
      </Button>
      <Button colorScheme="blue" onClick={() => onEditar({ structure, schematization })} isLoading={isLoading}>
        Salvar Edição / Avançar
      </Button>
    </Box>
  );
}
