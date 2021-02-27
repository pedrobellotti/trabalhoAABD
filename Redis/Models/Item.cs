using System;
using System.Collections.Generic;
using System.ComponentModel.DataAnnotations;
using System.Linq;
using System.Web;

namespace Redis.Models
{
    public class Item
    {
        [Key]
        public int codItem { get; set; }
        public string nomeItem { get; set; }
    }
}