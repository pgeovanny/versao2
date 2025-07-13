import React, { useState } from "react";
import { Box, Input, Button, Text, VStack, Spinner } from "@chakra-ui/react";
import { uploadPdf } from "../api";
import { Section } from "../types";

interface Props {
  onSuccess: (data: { structure: Section[]; pdfFile: File; pdfUrl: string }) => void;
}

const UploadPDF: React.FC<Props> = ({ onSuccess }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setError("");
    const file = e.target.files?.[0];
    if (file && file.type !== "application/pdf") {
      setError("Selecione um arquivo PDF.");
      return;
    }
    setSelectedFile(file || null);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    setIsUploading(true);
    setError("");
    try {
      const data = await uploadPdf(selectedFile);
      if (!data.structure || data.structure.length === 0) {
        setError("Não foi possível extrair o texto do PDF.");
      } else {
        onSuccess({ structure: data.structure, pdfFile: selectedFile, pdfUrl: "" });
      }
    } catch {
      setError("Erro ao fazer upload do PDF.");
    }
    setIsUploading(false);
  };

  return (
    <VStack spacing={4}>
      <Input type="file" accept="application/pdf" onChange={handleFileChange} />
      {selectedFile && (
        <Text fontSize="sm" color="gray.500">
          Selecionado: {selectedFile.name}
        </Text>
      )}
      <Button colorScheme="blue" onClick={handleUpload} isLoading={isUploading} isDisabled={!selectedFile}>
        Enviar PDF
      </Button>
      {error && <Text color="red.500">{error}</Text>}
      {isUploading && <Spinner />}
    </VStack>
  );
};

export default UploadPDF;
