    function filteredLines = ProgramaTexto2(imagePath)
    % CARGAR LA IMAGEN
    img = imread(imagePath);
    
    % Convertir a escala de grises si es necesario
    if size(img, 3) == 3
        grayImg = rgb2gray(img);
    else
        grayImg = img;
    end
    
    % PREPROCESAMIENTO DE LA IMAGEN
    adjustedImg = imadjust(grayImg); % Ajuste de contraste
    denoisedImg = medfilt2(adjustedImg); % Eliminación de ruido
    enhancedImg = adapthisteq(denoisedImg); % Mejora de contraste
    binaryImg = imbinarize(enhancedImg, 'adaptive', 'Sensitivity', 0.4); % Binarización
    
    % APLICAR OCR
    ocrResults = ocr(binaryImg, 'Language', 'spanish', 'TextLayout', 'Block');
    recognizedText = ocrResults.Text;
    
    % MOSTRAR EL TEXTO RECONOCIDO
    disp('Texto reconocido:');
    disp(recognizedText);
    
    % LIMPIAR Y DIVIDIR EL TEXTO RECONOCIDO
    textLines = strsplit(recognizedText, '\n'); % Dividir en líneas
    cleanedText = erase(textLines, {'\n', '?'}); % Eliminar caracteres no deseados
    
    % PALABRAS CLAVE PARA FILTRAR
    keywords = ["edad", "numero", "nombre", "medicamentos", "medicamento", ...
                "fecha", "cita", "familiar", "paciente", "tabletas", "solucion", ...
                "hora", "dias", "profesional"];
    
    % FILTRAR LÍNEAS CON PALABRAS CLAVE
    filteredLines = {};
    for i = 1:length(cleanedText)
        line = cleanedText{i};
        for j = 1:length(keywords)
            if contains(line, keywords(j), 'IgnoreCase', true)
                filteredLines{end+1} = line;
                break;
            end
        end
    end
    
    % CREAR UN ARCHIVO EXCEL CON EL TEXTO FILTRADO
    filteredTable = table(filteredLines', 'VariableNames', {'FilteredText'});
    filteredOutputFile = 'texto_filtrado.xlsx';
    writetable(filteredTable, filteredOutputFile);
    disp(['El texto filtrado se ha guardado en el archivo: ', filteredOutputFile]);
end
