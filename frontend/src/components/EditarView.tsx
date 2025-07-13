import React, { useState } from "react";
import { Box, Button, VStack, Textarea, Text, Divider } from "@chakra-ui/react";
import { Section, SchematizedSection } from "../types";

interface Props {
  structure: Section[];
  schematization: SchematizedSection[];
  onEditar: (editado: { structure: Section[]; schematization: SchematizedSection[] }) => void;
  isLoading: boolean;
  onBack: () => void;
}

const EditarView: React.FC<Props> = ({ structure, schematization, onEditar, isLoading, onBack }) => {
  const [edits, setEdits] = useState<SchematizedSection[]>(schematization);

  const handleEdit = (idx: number, value: string) => {
    const newEdits = [...edits];
    newEdits[idx] = { ...newEdits[idx], schematization: value };
    setEdits(newEdits);
  };

  return (
    <Box>
      <VStack align="stretch" spacing={4} mb={4}>
        <Text fontWeight="bold">Edite o esquema dos artigos abaixo:</Text>
        <Box maxH="400px" overflowY="auto" borderWidth={1} borderRadius="md" p={2}>
          {edits.map((sec, idx) => (
            <Box key={idx} mb={4}>
              <Text fontWeight="semibold" mb={2}>{sec.title}</Text>
              <Textarea
                minH="80px"
                value={sec.schematization}
                onChange={e => handleEdit(idx, e.target.value)}
                fontSize="sm"
                bg="gray.50"
                mb={2}
              />
              <Divider my={2} />
            </Box>
          ))}
        </Box>
      </VStack>
      <Button colorScheme="blue" onClick={() => onEditar({ structure, schematization: edits })} isLoading={isLoading} mr={2}>
        Salvar Edição & Avançar
      </Button>
      <Button onClick={onBack} variant="ghost">
        Voltar
      </Button>
    </Box>
  );
};

export default EditarView;
