import React, { useState } from "react";
import { Box, Heading, Container, Stepper, Step, StepIndicator, StepStatus, StepTitle, StepDescription, StepSeparator, Button, useToast } from "@chakra-ui/react";
import UploadPDF from "./components/UploadPDF";
import EstruturaView from "./components/EstruturaView";
import EsquematizacaoView from "./components/EsquematizacaoView";
import EditarView from "./components/EditarView";
import { Section, SchematizedSection } from "./types";

const steps = [
  { title: "PDF", description: "Envie o PDF da Lei" },
  { title: "Estrutura", description: "Visualize a estrutura extraída" },
  { title: "Esquematizar", description: "Organize e destaque com IA" },
  { title: "Editar", description: "Adicione questões e comentários" },
  { title: "Exportar", description: "Baixe o PDF final" },
];

function App() {
  const [activeStep, setActiveStep] = useState(0);
  const [structure, setStructure] = useState<Section[]>([]);
  const [schematization, setSchematization] = useState<SchematizedSection[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const toast = useToast();
  const [pdfFile, setPdfFile] = useState<File | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string>("");

  const nextStep = () => setActiveStep((s) => Math.min(s + 1, steps.length - 1));
  const prevStep = () => setActiveStep((s) => Math.max(s - 1, 0));

  // Voltar para o início
  const resetAll = () => {
    setActiveStep(0);
    setStructure([]);
    setSchematization([]);
    setPdfFile(null);
    setPdfUrl("");
  };

  return (
    <Container maxW="3xl" py={8}>
      <Heading mb={6} textAlign="center" fontWeight="bold">
        Lei Esquematizada
      </Heading>
      <Stepper size="md" index={activeStep} colorScheme="blue" mb={8}>
        {steps.map((step, idx) => (
          <Step key={idx}>
            <StepIndicator>
              <StepStatus complete={<Box bg="blue.400" w={4} h={4} borderRadius="full" />} active={<Box bg="blue.500" w={4} h={4} borderRadius="full" />} incomplete={<Box bg="gray.300" w={4} h={4} borderRadius="full" />} />
            </StepIndicator>
            <Box flexShrink={0}>
              <StepTitle>{step.title}</StepTitle>
              <StepDescription>{step.description}</StepDescription>
            </Box>
            <StepSeparator />
          </Step>
        ))}
      </Stepper>

      {/* Etapa 1: Upload PDF */}
      {activeStep === 0 && (
        <UploadPDF
          onSuccess={({ structure, pdfFile, pdfUrl }) => {
            setStructure(structure);
            setPdfFile(pdfFile);
            setPdfUrl(pdfUrl);
            toast({ title: "PDF extraído com sucesso!", status: "success" });
            nextStep();
          }}
        />
      )}

      {/* Etapa 2: Visualizar Estrutura */}
      {activeStep === 1 && (
        <EstruturaView
          structure={structure}
          onSumarizar={async (estrut) => {
            setIsLoading(true);
            try {
              const res = await fetch(`${import.meta.env.VITE_API_URL}/sumarizar/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ structure: estrut }),
              });
              const data = await res.json();
              setStructure(data.summarized || estrut);
              toast({ title: "Estrutura organizada!", status: "success" });
              nextStep();
            } catch (e) {
              toast({ title: "Erro ao organizar!", status: "error" });
            }
            setIsLoading(false);
          }}
          isLoading={isLoading}
          onBack={prevStep}
        />
      )}

      {/* Etapa 3: Esquematizar */}
      {activeStep === 2 && (
        <EsquematizacaoView
          structure={structure}
          onEsquematizar={async (estrut) => {
            setIsLoading(true);
            try {
              const res = await fetch(`${import.meta.env.VITE_API_URL}/esquematizar/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ structure: estrut }),
              });
              const data = await res.json();
              setSchematization(data.schematization || []);
              toast({ title: "Lei esquematizada!", status: "success" });
              nextStep();
            } catch (e) {
              toast({ title: "Erro ao esquematizar!", status: "error" });
            }
            setIsLoading(false);
          }}
          isLoading={isLoading}
          onBack={prevStep}
        />
      )}

      {/* Etapa 4: Editar */}
      {activeStep === 3 && (
        <EditarView
          structure={structure}
          schematization={schematization}
          onEditar={async (editado) => {
            setIsLoading(true);
            try {
              const res = await fetch(`${import.meta.env.VITE_API_URL}/editar/`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(editado),
              });
              const data = await res.json();
              setSchematization(data.edited || editado.schematization);
              toast({ title: "Edição salva!", status: "success" });
              nextStep();
            } catch (e) {
              toast({ title: "Erro ao editar!", status: "error" });
            }
            setIsLoading(false);
          }}
          isLoading={isLoading}
          onBack={prevStep}
        />
      )}

      {/* Etapa 5: Exportar PDF */}
      {activeStep === 4 && (
        <Box>
          <Button
            colorScheme="blue"
            size="lg"
            mb={4}
            isLoading={isLoading}
            onClick={async () => {
              setIsLoading(true);
              try {
                const res = await fetch(`${import.meta.env.VITE_API_URL}/exportar/`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({
                    structure,
                    schematization,
                    export_format: "pdf",
                  }),
                });
                const data = await res.json();
                if (data.file_url) {
                  window.open(data.file_url, "_blank");
                } else {
                  toast({ title: "Exportação realizada!", description: "Verifique o PDF final.", status: "success" });
                }
              } catch (e) {
                toast({ title: "Erro ao exportar PDF!", status: "error" });
              }
              setIsLoading(false);
            }}
          >
            Exportar PDF Final
          </Button>
          <Button variant="outline" ml={4} onClick={resetAll}>
            Recomeçar
          </Button>
        </Box>
      )}
    </Container>
  );
}

export default App;
