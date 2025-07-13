import React, { useRef, useState } from "react";
import { Box, Button, Input, Spinner, Text } from "@chakra-ui/react";
import { Section } from "../types";

type Props = {
  onSuccess: (args: { structure: Section[]; pdfFile: File | null; pdfUrl: string }) => void;
};

export default function UploadPDF({ onSuccess }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;
    setLoading(true);
    const formData = new FormData();
    formData.append("pdf", file);

    try {
      const res = await fetch(`${import.meta.env.VITE_API_URL}/extrair/`, {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      if (data.structure) {
        onSuccess({ structure: data.structure, pdfFile: file, pdfUrl: "" });
      }
    } catch {
      alert("Erro ao extrair PDF.");
    }
    setLoading(false);
  };

  return (
    <Box textAlign="center">
      <Input
        type="file"
        accept=".pdf"
        ref={inputRef}
        onChange={handleUpload}
        display="none"
      />
      <Button colorScheme="blue" onClick={() => inputRef.current?.click()} isLoading={loading}>
        Enviar PDF da Legislação
      </Button>
      <Text fontSize="sm" mt={4} color="gray.500">
        Envie o PDF da lei para começar.
      </Text>
    </Box>
  );
}
