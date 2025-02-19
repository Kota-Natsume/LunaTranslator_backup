﻿using System;
using System.IO;
using System.Threading.Tasks;
using Windows.Globalization;
using Windows.Graphics.Imaging;
using Windows.Media.Ocr;
using Windows.Storage;
using Windows.Storage.Streams;

namespace WinRTOCR
{
    class Program
    {
        static void Main(string[] args)
        {
            //#if DEBUG
            //            args = new string[] { "..\\..\\x.png" };
            //#endif
            //            string language = "zh-Hans-CN";
            string result = RecognizeAsync(args[1], args[0]).GetAwaiter().GetResult();


        }




        static async Task<string> RecognizeAsync(string imagePath, string language)
        {
            Console.OutputEncoding = System.Text.Encoding.UTF8;
            StorageFile storageFile;
            var path = Path.GetFullPath(imagePath); // x.png
            var extName = Path.GetExtension(path); // .png
            //var outPath = path.Replace(extName, "") + "-out" + extName;  // x-out.png
            storageFile = await StorageFile.GetFileFromPathAsync(path);
            IRandomAccessStream randomAccessStream = await storageFile.OpenReadAsync();
            Windows.Graphics.Imaging.BitmapDecoder decoder = await Windows.Graphics.Imaging.BitmapDecoder.CreateAsync(randomAccessStream);
            SoftwareBitmap softwareBitmap = await decoder.GetSoftwareBitmapAsync(BitmapPixelFormat.Bgra8, BitmapAlphaMode.Premultiplied);
            Language lang = new Language(language);
            string space = language.Contains("zh") || language.Contains("ja") ? "" : " ";
            string result = null;
            if (OcrEngine.IsLanguageSupported(lang))
            {
                OcrEngine engine = OcrEngine.TryCreateFromLanguage(lang);
                if (engine != null)
                {
                    OcrResult ocrResult = await engine.RecognizeAsync(softwareBitmap);
                     
                    result = ocrResult.Text;

                    foreach (var line in ocrResult.Lines)
                    {


                        string xx = "";
                        xx = line.Words[0].BoundingRect.Y.ToString() + " ";

                        foreach (var word in line.Words)
                        {
                            xx += (word.Text)+ space;
                        }
                        Console.WriteLine(xx);

                    }
                }
            }
            else
            {
                throw new Exception(string.Format("Language {0} is not supported", language));
            };
            softwareBitmap.Dispose();
            return await Task<string>.Run(() =>
            {
                return result;
            });
        }
    }
}

 
//using System;
//using System.Collections.Generic;
//using System.Drawing;
//using System.Drawing.Imaging;
//using System.Globalization;
//using System.IO;
//using System.Linq;
//using System.Text;
//using System.Text.RegularExpressions;
//using System.Threading.Tasks;
//using System.Windows;
//using System.Windows.Input;
//using System.Windows.Markup;
//using System.Windows.Media;
//using System.Windows.Media.Imaging;
//using Windows.Globalization;
//using Windows.Graphics.Imaging;
//using Windows.Media.Ocr;
//using BitmapDecoder = Windows.Graphics.Imaging.BitmapDecoder;

//namespace ConsoleApp1
//{
//    class Program
//    {
//        static void Main(string[] args)
//        { 
//            List<Language> possibleOcrLanguages = OcrEngine.AvailableRecognizerLanguages.ToList();
//            foreach(var l in possibleOcrLanguages)
//            {
//                Console.WriteLine(l.DisplayName);
//                Console.WriteLine(l.LanguageTag);
//            }
//        }
//    }
//}
