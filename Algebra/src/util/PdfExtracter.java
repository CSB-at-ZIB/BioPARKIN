/*
 * To change this template, choose Tools | Templates
 * and open the template in the editor.
 */

package util;
import java.io.File;
import java.io.FileInputStream;
//import java.io.IOException;

//import java.util.HashSet;

//import org.apache.pdfbox.pdfparser.PDFParser;
/**
 *
 * @author hendrik1
 */
public class PdfExtracter {
    private static final String NULL_STR = "null";
    private File pdfFile;
    private String title;
    public PdfExtracter (String pdfFile){
        this.pdfFile = new File (pdfFile);
    }
    public PdfExtracter (File pdfFile){
        this.pdfFile = pdfFile;
    }
    public String getTitle (){
        if(title==null){
            setTitle ();
            if(title==null) return NULL_STR;
            return title;
        } return title;
    }
    public void setTitle (){
        FileInputStream f = null;
        //TODO: fix library setting
        /*PDFParser p = null;
        try{
            f = new FileInputStream(pdfFile);
            p = new PDFParser (f);
            p.parse();
            title = p.getDocument().getHeaderString();
            f.close();
        } catch (IOException e){
            throw new RuntimeException (e.getMessage());
        }*/
    }
    public static void main (String[] args){
        Directory d = new Directory ("C:/Dokumente und Einstellungen/hendrik1/" +
                "Eigene Dateien/Papers/");
        RegexFileFilter r = new RegexFileFilter (".*.pdf");
        File[] pdfs = d.listFiles(r);
        for (int i = 0; i < pdfs.length; i++){
            PdfExtracter pdf = new PdfExtracter (pdfs[i]);
            pdf.setTitle();
            if(pdf.title!=null) System.out.println(pdf.getTitle());
        }
    }
}
