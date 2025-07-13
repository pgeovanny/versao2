import axios from "axios";

const API_URL = import.meta.env.VITE_API_URL;

export const uploadPdf = async (pdfFile: File) => {
  const formData = new FormData();
  formData.append("pdf", pdfFile);
  const response = await axios.post(`${API_URL}/extrair/`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
};
