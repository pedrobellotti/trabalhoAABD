using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Data.Entity;

namespace Redis.Models
{
    public class Contexto: DbContext
    {
        public DbSet<Item> Itens { get; set; }

    }
}